import { useState } from "react";

import Map, { Marker, Popup } from "react-map-gl/maplibre";

import { MapPin } from "lucide-react";

import "maplibre-gl/dist/maplibre-gl.css";

import { usePosts } from "../../features/posts/hooks/usePosts";

import type { Post } from "../../features/posts/types";

export function PostsMap() {
  const { data: posts, isLoading } = usePosts();

  const [selectedPost, setSelectedPost] = useState<Post | null>(null);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Map
      initialViewState={{
        longitude: 8.5417,
        latitude: 47.3769,
        zoom: 3,
      }}
      style={{ width: "100%", height: "100%" }}
      mapStyle="https://demotiles.maplibre.org/style.json"
    >
      {posts?.map((post) => (
        <Marker
          key={post.id}
          longitude={post.longitude}
          latitude={post.latitude}
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
              setSelectedPost(post);
            }}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: 0,
            }}
          >
            <MapPin
              color={selectedPost?.id === post.id ? "green" : "black"}
              size={32}
            />
          </button>
        </Marker>
      ))}

      {selectedPost && (
        <Popup
          longitude={selectedPost.longitude}
          latitude={selectedPost.latitude}
          anchor="top"
          onClose={() => setSelectedPost(null)}
        >
          <div
            style={{
              maxWidth: 200,
            }}
          >
            <p
              style={{
                margin: 0,
              }}
            >
              {selectedPost.caption}
            </p>
          </div>
        </Popup>
      )}
    </Map>
  );
}
