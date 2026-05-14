import Map, { Marker, Popup } from "react-map-gl/maplibre";

import "maplibre-gl/dist/maplibre-gl.css";

import { usePosts } from "../../features/posts/hooks/usePosts";

export function PostsMap() {
  const { data: posts, isLoading } = usePosts();

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
        />
      ))}
    </Map>
  );
}
