from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import Round, RollLog, RoundLog, ActivityLog
from .forms import RoundForm
from django.http import JsonResponse

IN_ROUND_LIST = []   # список с участниками текущего раунда


def home(request):
    x = 15
    context = {'x': x}
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            ActivityLog.objects.create(user=new_user)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def cabinet(request):
    return render(request, 'cabinet.html')


def game(request):
    global IN_ROUND_LIST

    if not Round.objects.all():
        # настройка БД перед первым раундом
        Round.objects.create()
        for x in range(1, 12):
            # прогонка нулевого раунда...
            RoundForm.turn(Round.objects.last())
            RollLog.objects.create(user=request.user,
                                   roll_round=Round.objects.last(),
                                   roll_num='jackpot')
        Round.objects.create()  # ...и создание первого раунда
    if not RoundLog.objects.exists():
        RoundLog.objects.create(round_num=Round.objects.last(), players_amount=0)  # создание нулевой модели лога
    previous_roll = getattr(RollLog.objects.last(), 'roll_num')
    round_n = RoundLog.objects.last().round_num  # номер текущего раунда
    players_a = RoundLog.objects.last().players_amount  # и кол-во участников

    if request.method == 'POST':
        # *Игрок прокрутил рулетку*
        # В БД по мере необходимости уходят разные логи
        active_user = ActivityLog.objects.get(user=request.user)
        active_user.rolls_amount += 1
        active_user.save()
        active_user.save(update_fields=['rolls_amount'])

        if request.user not in IN_ROUND_LIST:
            # Проверка - зачислен ли сходивший игрок в участники раунда
            IN_ROUND_LIST.append(request.user)
            active_user.rounds_amount += 1
            active_user.save()

        rolled_point = RoundForm.turn(Round.objects.last())
        if rolled_point == 'jackpot!':
            RoundLog.objects.update(round_num=Round.objects.last(),
                                    players_amount=len(IN_ROUND_LIST))
            IN_ROUND_LIST.clear()
            RollLog.objects.create(user=request.user,
                                   roll_round=Round.objects.last(),
                                   roll_num='jackpot')
            Round.objects.create()
            RoundLog.objects.create(round_num=Round.objects.last(),
                                    players_amount=0)
        else:
            RollLog.objects.create(user=request.user,
                                   roll_round=Round.objects.last(),
                                   roll_num=str(rolled_point))
            RoundLog.objects.update(round_num=Round.objects.last(),
                                    players_amount=len(IN_ROUND_LIST))
        return JsonResponse({"rolled_point": rolled_point}, status=200)

    elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # запрос данных из БД и формирование JSON-ответа
        # для фонового обновления данных у игроков
        # после получения интервального ajax-запроса
        round_n = str(RoundLog.objects.last().round_num)
        players_a = str(RoundLog.objects.last().players_amount)
        top_activity_list = [instance for instance in ActivityLog.objects.all().order_by('-rounds_amount')[:5]]
        all_top = []
        for obj in top_activity_list:
            temp = [0, 1, 2]
            temp[0] = str(obj.id)
            temp[1] = str(obj.rounds_amount)
            if obj.rounds_amount > 0:
                rolls_per_round = obj.rolls_amount // obj.rounds_amount
            else:
                rolls_per_round = 0
            temp[2] = str(rolls_per_round)
            all_top.append(temp)
        return JsonResponse({'round_n': round_n, 'players_a': players_a, 'all_top': all_top}, status=200)

    context = {
        'previous_roll': previous_roll,
        'round_n': round_n,
        'players_a': players_a,
        }
    return render(request, 'game.html', context)





