from sqlalchemy import select

from fast_training.models import User


def test_create_user(session):
    new_user = User(username='testdan', password='testsenha', email='test@email.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testdan'))

    assert user.username == 'testdan'
