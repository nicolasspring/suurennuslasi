import { useQuery } from "@tanstack/react-query";

import { getPosts } from "../../../api/posts";

export function usePosts() {
  return useQuery({
    queryKey: ["posts"],
    queryFn: getPosts,
  });
}
