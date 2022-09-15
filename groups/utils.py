from .models import TransferToMake, GroupUser, CashMovement


def get_min(arr, nr):
    min_ind = 0
    for i in range(1, nr):
        if arr[i] < arr[min_ind]:
            min_ind = i
    return min_ind


def get_max(arr, nr):
    max_ind = 0
    for i in range(1, nr):
        if arr[i] > arr[max_ind]:
            max_ind = i
    return max_ind


def min_of_2(x, y):
    return x if x < y else y


# distribution of the cash owed between group users - recursive function
def min_cash_flow_rec(grp_users, balances):
    nr = len(balances)

    max_credit = get_max(balances, nr)
    max_debit = get_min(balances, nr)

    smallest = min_of_2(-balances[max_debit], balances[max_credit])
    balances[max_credit] = round(balances[max_credit] - smallest, 2)
    balances[max_debit] = round(balances[max_debit] + smallest, 2)

    TransferToMake.objects.create(
        sender=grp_users[max_debit],
        receiver=grp_users[max_credit],
        amount=smallest,
        group=grp_users[0].group,
    )
    min_cash_flow_rec(grp_users, balances)


# Recalculated owed amounts when there is a change in group expenses
def manage_transfers(group):
    TransferToMake.objects.filter(group=group).delete()
    grp_users = GroupUser.objects.filter(group=group)
    balances = [user.balance for user in grp_users]
    min_cash_flow_rec(grp_users, balances)


def track_cash_movements(expense, updated_borrowers):
    split_amount = round(expense.price / len(updated_borrowers), 2)

    lent = round(expense.price - split_amount, 2) if expense.paid_by in updated_borrowers else round(expense.price, 2)
    if expense.price % split_amount:
        last_split = round(expense.price - split_amount * (len(updated_borrowers) - 1), 2)
    else:
        last_split = 0

    for user in updated_borrowers:
        if last_split and user != expense.paid_by:
            user.balance = round(user.balance - last_split, 2)
            CashMovement.objects.create(group_user=user, expense=expense, balance_impact=-last_split)
            last_split = 0
        elif user != expense.paid_by:
            user.balance = round(user.balance - split_amount, 2)
            CashMovement.objects.create(group_user=user, expense=expense, balance_impact=-split_amount)
        user.save()

    lender = GroupUser.objects.get(id=expense.paid_by.id)
    lender.balance = round(lender.balance + lent, 2)
    CashMovement.objects.create(group_user=expense.paid_by, expense=expense, balance_impact=lent)
    lender.save()

    manage_transfers(expense.group)
