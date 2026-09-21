"""UserTableSeeder Seeder."""

from masoniteorm.seeds import Seeder

from app.models.User import User


class UserTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        User.create(
            {
                "name": "Masonite",
                "email": "user@example.com",
                "password": "secret",
            }
        )
