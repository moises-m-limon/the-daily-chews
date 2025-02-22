"use client";

import type React from "react";
import { useState, useRef } from "react";
import { Image, X, Video } from "lucide-react";

interface CreatePostProps {
  addPost: (post: { username: string; mediaUrl: string; caption: string; mediaType: "image" | "video" }) => void;
}

export default function CreatePost({ addPost }: CreatePostProps) {
  const [username, setUsername] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");
  const [caption, setCaption] = useState("");
  const [preview, setPreview] = useState("");
  const [mediaType, setMediaType] = useState<"image" | "video" | "">("");

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (username && mediaUrl && caption) {
      addPost({ username, mediaUrl, caption, mediaType: mediaType as "image" | "video" });
      setUsername("");
      setMediaUrl("");
      setCaption("");
      setPreview("");
      setMediaType("");
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const url = e.target.value;
    setMediaUrl(url);
    setPreview(url);
    setMediaType(url.match(/\.(mp4|webm|ogg)$/i) ? "video" : "image");
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleFile = (file: File) => {
    const fileURL = URL.createObjectURL(file);
    setPreview(fileURL);
    setMediaUrl(fileURL);
    setMediaType(file.type.startsWith("video") ? "video" : "image");
  };

  return (
    <form onSubmit={handleSubmit} className="create-post">
      <div className="create-post-header">
        <h2>Create new post</h2>
      </div>

      <div 
        className="create-post-form"
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        {preview ? (
          <div className="create-post-preview">
            {mediaType === "video" ? (
              <video src={preview} controls className="media-preview" style={{"width": "100%"}} />
            ) : (
              <img src={preview} alt="Preview" className="media-preview" />
            )}
            <button type="button" onClick={() => { setPreview(""); setMediaUrl(""); setMediaType(""); }} className="post-button">
              <X className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div 
            className="create-post-placeholder"
            onClick={() => fileInputRef.current?.click()}
          >
            <Image className="w-20 h-20" />
            <p>Drag photos and videos here or click to upload</p>
          </div>
        )}

        <input 
          type="file" 
          accept="image/*,video/*"
          ref={fileInputRef} 
          className="hidden" 
          onChange={handleFileChange} 
        />

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="create-post-input"
          required
        />

        <input
          type="url"
          placeholder="Paste image or video URL"
          value={mediaUrl}
          onChange={handleUrlChange}
          className="create-post-input"
        />

        <textarea
          placeholder="Write a caption..."
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          className="create-post-textarea"
          required
        ></textarea>

        <button type="submit" className="create-post-button">
          Share
        </button>
      </div>
    </form>
  );
}
