"use client";

import { useEffect, useRef, useState } from "react";
import { Heart, MessageCircle, Send, Bookmark, Volume2, VolumeX } from "lucide-react";

interface PostProps {
  username: string;
  mediaUrl: string;
  caption: string;
  likes: number;
  mediaType: "image" | "video";
}

export default function Post({ username, mediaUrl, caption, likes, mediaType }: PostProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isMuted, setIsMuted] = useState(true);
  const [isVisible, setIsVisible] = useState(false);

  // Function to toggle mute/unmute
  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !videoRef.current.muted;
      setIsMuted(videoRef.current.muted);
    }
  };

  // Observer to auto-play when in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
            if (videoRef.current) {
              videoRef.current.play();
            }
          } else {
            setIsVisible(false);
            if (videoRef.current) {
              videoRef.current.pause();
            }
          }
        });
      },
      { threshold: 0.8 }
    );

    if (videoRef.current) {
      observer.observe(videoRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <article className={`post-reel ${isVisible ? "active" : ""}`}>
      <div className="post-reel-header">
        <div className="post-avatar">
          <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${username}`} alt={username} />
        </div>
        <span className="post-username">{username}</span>
      </div>

      {/* Post Media (Reels Style) */}
      <div className="post-reel-media">
        {mediaType === "video" ? (
          <video
            class-
            ref={videoRef}
            src={mediaUrl}
            className="post-reel-video"
            loop
            muted
            playsInline
          />
        ) : (
          <img src={mediaUrl} alt={caption} className="post-reel-image" />
        )}

        {/* Mute/Unmute Button */}
        
      </div>

      {/* Post Actions */}
      <div className="post-reel-actions">
        <button className="post-button">
          <Heart className="w-6 h-6" />
        </button>
        {mediaType === "video" && (
          <button onClick={toggleMute} className="reel-mute-btn">
            {isMuted ? <VolumeX className="w-6 h-6" /> : <Volume2 className="w-6 h-6" />}
          </button>
        )}
        <button className="post-button">
          <MessageCircle className="w-6 h-6" />
        </button>
        <button className="post-button">
          <Send className="w-6 h-6" />
        </button>
        <button className="post-button">
          <Bookmark className="w-6 h-6" />
        </button>
      </div>

      {/* Likes & Caption */}
      <div className="post-reel-info">
        <div className="post-likes">{likes.toLocaleString()} likes</div>
        <div className="post-caption">
          <span className="post-caption-username">{username}</span> {caption}
        </div>
      </div>
    </article>
  );
}
