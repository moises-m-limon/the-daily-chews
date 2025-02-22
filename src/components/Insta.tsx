"use client";

import { useState } from "react";
import Header from "./Header";
import Feed from "./Feed";
import CreatePost from "./CreatePost";

interface Post {
  id: number;
  username: string;
  mediaUrl: string;
  caption: string;
  likes: number;
  mediaType: "image" | "video";
}

export default function InstagramClone() {
  const [posts, setPosts] = useState<Post[]>([
    {
      id: 1,
      username: "johndoe",
      mediaUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
      caption: "Nature vibes 🌿🍃",
      likes: 1540,
      mediaType: "video",
    },
    {
      id: 2,
      username: "janedoe",
      mediaUrl: "https://picsum.photos/id/2/500/500",
      caption: "Delicious food! 🍕 #foodie #yummy",
      likes: 856,
      mediaType: "image",
    },
    {
      id: 3,
      username: "traveler",
      mediaUrl: "https://www.w3schools.com/html/movie.mp4",
      caption: "Exploring the world 🌎",
      likes: 2023,
      mediaType: "video",
    },
  ]);

  const addPost = (post: Omit<Post, "id" | "likes">) => {
    setPosts([
      {
        ...post,
        id: posts.length + 1,
        likes: 0,
      },
      ...posts,
    ]);
  };

  return (
    <div className="insta-app">
      <Header />
      <CreatePost addPost={addPost} />
      <Feed posts={posts} />
    </div>
  );
}
