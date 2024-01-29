import { useEffect, useState } from "react";
import Comment from "./Comment";

interface CommentProps {
  product: number;
}

interface CommentData {
  product: number;
  body: string;
  created_on: Date;
  owner: string;
}

const CommentSection = ({ product }: CommentProps) => {
  const [comments, setComments] = useState<CommentData[]>([]);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/comment/`);
        const data = await response.json();

        console.log("Received data from server:", data);

        if (Array.isArray(data)) {
          const filteredComments = data.filter(
            (comment: CommentData) => comment.product === product
          );

          console.log("Filtered comments:", filteredComments);
          console.log("Filtered comments id:", product);

          setComments(filteredComments || []);
        } else {
          console.error("Invalid data structure received from server");
        }
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    };

    fetchComments();
  }, [product]);

  return (
    <div className="mb-4">
      <h2 className="m-4 text-2xl font-bold">Comments</h2>
      <ul className="comoverflow-y-auto gap-1">
        {comments.map((comment) => (
          <li key={comment.product}>
            <Comment
              owner={comment.owner}
              body={comment.body}
              created_on={comment.created_on}
            />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CommentSection;
