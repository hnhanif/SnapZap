from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ConversationMessageForm
from item.models import Item
from .models import Conversation
# Create your views here.


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    form = ConversationMessageForm()
    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(
        item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect("conversation:chat-detail", pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    return render(request, 'conversation/chat.html', context={'form': form})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', context={"conversations": conversations})


@login_required
def inbox_detail(request, pk):
    form = ConversationMessageForm()
    conversation = Conversation.objects.filter(
        members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            covnersation_message = form.save(commit=False)
            covnersation_message.conversation = conversation
            covnersation_message.created_by = request.user
            covnersation_message.save()

            conversation.save()
            return redirect('conversation:chat-detail', pk=pk)
    return render(request, 'conversation/chat_detail.html', context={'conversation': conversation, "form": form})
