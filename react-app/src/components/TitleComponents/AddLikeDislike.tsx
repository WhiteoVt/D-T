import { useAuth } from "../../AuthContext";
import { useState, useEffect } from "react";

interface Props {
  id: number;
  liked: number;
  upvotes: number;
  downvotes: number;
  onVoteSubmitted: () => void;
}

const AddLikeDislike = ({
  id,
  liked,
  upvotes,
  downvotes,
  onVoteSubmitted,
}: Props) => {
  const { token } = useAuth();
  const [isLiked, setIsLiked] = useState<number | null>(liked);
  const [isInCollection, setIsInCollection] = useState<boolean>(false);

  const checkIfInCollection = async (idToCheck: number) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/ownedproduct/${idToCheck}/`,
        {
          method: "GET",
          headers: {
            accept: "application/json",
            Authorization: `token ${token}`,
          },
        }
      );

      if (response.ok) {
        setIsInCollection(true);
      } else {
        setIsInCollection(false);
      }
    } catch (error) {
      console.error("Error checking if in collection:", error);
    }
  };

  useEffect(() => {
    setIsLiked(liked);
    checkIfInCollection(id);
  }, [id]);

  const handleAdd = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/ownedproduct/`, {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `token ${token}`,
        },
        body: JSON.stringify({
          product: id,
        }),
      });

      if (response.ok) {
        console.log("Product added successfully");

        setIsInCollection(true);
      } else {
        const errorData = await response.json();
        console.error("Adding product failed:", errorData);
      }
    } catch (error) {
      console.error("Error during adding product:", error);
    }
  };

  const handleVote = async (vote: number) => {
    try {
      const newVote = isLiked === vote ? 0 : vote;

      const response = await fetch(`http://localhost:8000/api/vote/`, {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `token ${token}`,
        },
        body: JSON.stringify({
          product: id,
          value: newVote,
        }),
      });

      if (response.ok) {
        console.log("Vote submitted successfully");

        setIsLiked(newVote);

        onVoteSubmitted();
      } else {
        const errorData = await response.json();
        console.error("Voting failed:", errorData);
      }
    } catch (error) {
      console.error("Error during voting:", error);
    }
  };

  const likeStyle = (value: number | null) => {
    switch (value) {
      case 2:
        return "bg-blue-500 text-white";
      default:
        return "bg-blue-300 text-white";
    }
  };
  const dislikeStyle = (value: number | null) => {
    switch (value) {
      case 1:
        return "bg-blue-500 text-white";
      default:
        return "bg-blue-300 text-white";
    }
  };

  const addToCollectionStyle = () =>
    isInCollection ? "bg-red-500 text-white" : "bg-blue-500 text-white";

  const addToCollectionText = () =>
    isInCollection ? "Is in your collection" : "Add to your collection";

  return (
    <div className="grid grid-cols-12 mb-10">
      <p className="col-span-6 mb-2" />
      <p className="col-span-2 text-center">Up votes &#x1F44D; {upvotes}</p>
      <p className="col-span-1" />
      <p className="col-span-2 text-center">{downvotes} &#x1F44E; Down votes</p>
      <button
        className={`col-span-4 p-2 rounded-md mt-2 ${addToCollectionStyle()}`}
        onClick={handleAdd}
      >
        {addToCollectionText()}
      </button>
      <p className="col-span-2" />
      <button
        className={`col-span-2 p-2 rounded-md mt-2 ${likeStyle(isLiked)}`}
        onClick={() => handleVote(2)}
      >
        Like
      </button>
      <p className="col-span-1" />
      <button
        className={`col-span-2 p-2 rounded-md mt-2 ${dislikeStyle(isLiked)}`}
        onClick={() => handleVote(1)}
      >
        Dislike
      </button>
    </div>
  );
};

export default AddLikeDislike;
