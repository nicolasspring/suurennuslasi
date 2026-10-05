import { useQuery } from "@tanstack/react-query";

import { getPosts } from "../../../api/posts";

interface UsePostsOptions {
  enabled?: boolean;
  refetchInterval?: number | false;
}

export function usePosts({
  enabled = true,
  refetchInterval,
}: UsePostsOptions = {}) {
  return useQuery({
    queryKey: ["posts"],
    queryFn: getPosts,
    enabled,
    refetchInterval,
  });
}
