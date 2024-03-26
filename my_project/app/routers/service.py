from sqlalchemy.orm import Session
from my_project.app import models
from my_project.app.routers.email import email_service

def send_notifications_to_users(db: Session, new_post: models.Advert):
    # Get all users from the database
    users = db.query(models.User).all()

    # Extract email addresses of all users
    user_emails = [user.email for user in users]

    # Compose email content
    subject = "New post notification"
    body = f"A new post has been created: {new_post.title}. Check it out on the platform!"

    # Send email notifications
    email_service.send_email(user_emails, subject, body)