# community_tools/forums.py

from datetime import datetime
from typing import List, Dict, Optional

class ForumPost:
    def __init__(self, post_id: int, user_id: str, title: str, content: str):
        self.post_id = post_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.comments: List[Dict] = []  # List to hold comments

    def add_comment(self, user_id: str, comment: str):
        comment_data = {
            'user_id': user_id,
            'comment': comment,
            'created_at': datetime.now()
        }
        self.comments.append(comment_data)

    def get_post_details(self) -> Dict:
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'comments': self.comments
        }

class CommunityForum:
    def __init__(self):
        self.forums: Dict[str, List[ForumPost]] = {}  # Dictionary to hold forums and their posts
        self.forum_id_counter = 0  # Counter for unique forum IDs

    def create_forum(self, forum_name: str):
        if forum_name not in self.forums:
            self.forums[forum_name] = []
            print(f"Forum '{forum_name}' created successfully.")
        else:
            print(f"Forum '{forum_name}' already exists.")

    def create_post(self, forum_name: str, user_id: str, title: str, content: str) -> Optional[int]:
        if forum_name not in self.forums:
            print(f"Forum '{forum_name}' does not exist.")
            return None

        self.forum_id_counter += 1
        new_post = ForumPost(post_id=self.forum_id_counter, user_id=user_id, title=title, content=content)
        self.forums[forum_name].append(new_post)
        print(f"Post '{title}' created successfully in forum '{forum_name}'.")
        return new_post.post_id

    def add_comment(self, forum_name: str, post_id: int, user_id: str, comment: str):
        if forum_name not in self.forums:
            print(f"Forum '{forum_name}' does not exist.")
            return

        for post in self.forums[forum_name]:
            if post.post_id == post_id:
                post.add_comment(user_id, comment)
                print(f"Comment added to post ID {post_id} in forum '{forum_name}'.")
                return

        print(f"Post ID {post_id} not found in forum '{forum_name}'.")

    def get_forum_posts(self, forum_name: str) -> List[Dict]:
        if forum_name not in self.forums:
            print(f"Forum '{forum_name}' does not exist.")
            return []

        return [post.get_post_details() for post in self.forums[forum_name]]

    def moderate_post(self, forum_name: str, post_id: int, action: str):
        if forum_name not in self.forums:
            print(f"Forum '{forum_name}' does not exist.")
            return

        for post in self.forums[forum_name]:
            if post.post_id == post_id:
                if action == 'delete':
                    self.forums[forum_name].remove(post)
                    print(f"Post ID {post_id} deleted from forum '{forum_name}'.")
                elif action == 'edit':
                    new_content = input("Enter new content for the post: ")
                    post.content = new_content
                    print(f"Post ID {post_id} edited successfully.")
                return

        print(f"Post ID {post_id} not found in forum '{forum_name}'.")

# Example usage
if __name__ == "__main__":
    community_forum = CommunityForum()
    community_forum.create_forum("General Discussion")
    post_id = community_forum.create_post("General Discussion", "user123", "Welcome!", "Hello everyone!")
    community_forum.add_comment("General Discussion", post_id, "user456", "Hi there!")
    posts = community_forum.get_forum_posts("General Discussion")
    print(posts)
