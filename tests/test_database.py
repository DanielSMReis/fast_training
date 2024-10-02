from sqlalchemy import select

from fast_training.models import Todo, User


def test_create_user(session):
    new_user = User(username='testdan', password='testsenha', email='test@email.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testdan'))

    assert user.username == 'testdan'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Title',
        description='Test description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
