from django.views.generic.detail import DetailView

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from groups.models import *

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@method_decorator(login_required, name='dispatch')
class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group.html'

    def dispatch(self, request, *args, **kwargs):
        group = Group.objects.get(id=self.kwargs['pk'])

        # check permission
        try:
            GroupUser.objects.get(group=group, profile=self.request.user.profile)
        except GroupUser.DoesNotExist:
            raise PermissionDenied("You can't access the group")
        return super(GroupDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        group = Group.objects.get(id=self.kwargs['pk'])
        context['logged_user'] = self.request.user.profile
        context['group_users'] = GroupUser.objects.filter(group=group)
        context['cash_transfers'] = TransferToMake.objects.filter(group=group)
        context['group_data'] = group

        user_groups = Group.objects.filter(profile=self.request.user.profile).order_by('-last_update')
        context['current_group_id'] = group.id
        context['user_groups'] = user_groups

        # pagination
        expenses = Expense.objects.filter(group=group).order_by('-paid_date')

        page = self.request.GET.get('page')
        el_per_page = 11
        left_right_pages_range = 2
        paginator = Paginator(expenses, el_per_page)

        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            expenses = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            expenses = paginator.page(page)

        left_index = int(page) - left_right_pages_range
        if left_index < 1:
            left_index = 1
        right_index = int(page) + left_right_pages_range + 1
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages + 1

        page_range = range(left_index, right_index)

        context['group_expenses'] = expenses
        context['custom_range'] = page_range

        self.request.session['group_id'] = str(group.id)
        return context