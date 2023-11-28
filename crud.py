import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def get_users_with_posts(
        session: AsyncSession
):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    # users = await session.scalars(stmt)
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:  # type: User
        print("**" * 3)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print('**' * 10)
        print(post, post)
        print("author", post.user)


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(f"User", user)
        print(f"first_name", user.profile and user.profile.first_name)


async def show_users_with_post_and_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile), selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(f"User", user)
        print(f"first_name", user.profile and user.profile.first_name)
        for post in user.posts:
            print("post", post)
        print("**" * 10)


async def create_post(
        session: AsyncSession,
        user_id: int,
        *post_titles: str
) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in post_titles
    ]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_profiles_with_users_and_users_whit_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts)
        )
        .where(User.username == 'Alex')
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:  # type Profile
        print('Profile', profile.first_name)
        print('User', profile.user)
        print('Post', profile.user.posts)
        print('**' * 10)


async def main_relations(session):
    await create_user(session=session, username="Alex")
    await create_user(session=session, username="Alice")
    await create_user(session=session, username="Roman")
    user_alex = await get_user_by_username(session=session, username="Alex")
    user_roman = await get_user_by_username(session=session, username="Roman")

    await create_profile(session=session, user_id=user_alex.id, first_name=user_alex.username)
    await create_profile(
        session=session,
        user_id=user_roman.id,
        first_name=user_roman.username,
        last_name="White",
    )
    print()
    await show_users_with_profiles(session=session)
    await create_post(
        session,
        user_alex.id,
        "SQLA 2.0",
        "SQLA Joins",
        "Hello world",
    )
    await create_post(
        session,
        user_roman.id,
        "FastAPI first",
        "FastAPI next 3.20",
    )
    await get_profiles_with_users_and_users_whit_posts(session=session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        pass


if __name__ == "__main__":
    asyncio.run(main())
