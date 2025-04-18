TagDetail = """
query TagDetail($tagName: String!, $after: Cursor) {
  tag(tagName: $tagName) {
    name
    followingCount
    assets {
      backgroundImage {
        location
        __typename
      }
      detailBackgroundImage {
        location
        __typename
      }
      __typename
    }
    users(after: $after) {
      totalCount
      edges {
        node {
          id
          username
          assets {
            image {
              location
              __typename
            }
            __typename
          }
          followStatus
          protectedFields {
            ... on UserProtectedFields {
              totalWorkoutCounts
              __typename
            }
            ... on UserPrivacyError {
              code
              message
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      pageInfo {
        hasNextPage
        endCursor
        __typename
      }
      __typename
    }
    __typename
  }
}
"""
