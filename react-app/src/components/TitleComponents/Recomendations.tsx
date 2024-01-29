import { useEffect, useState } from "react";
import { useAuth } from "../../AuthContext";
import { Link } from "react-router-dom";
import { FaSpinner } from "react-icons/fa";

interface Props {
  id: number;
}

interface Recommendation {
  product_id: number;
  product_name: string;
  product_thumbnail: string;
  product_slug: string;
}

const Recommendations = ({ id }: Props) => {
  const { token } = useAuth();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      setIsLoading(true);

      const response = await fetch(`http://localhost:8002/recommend/${id}/`, {
        method: "GET",
        headers: {
          accept: "application/json",
          Authorization: `token ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setRecommendations(data.co_occurrence_recommendations || []);
        console.log("Dane pobrane z serwera:", data);

        setIsLoading(false);
      } else {
        console.error("Błąd w strukturze danych:", response);
      }
    } catch (error) {
      console.error("Błąd pobierania danych:", error);
    }
  };

  useEffect(() => {
    fetchData();
    window.scrollTo(0, 0);
  }, [id, token]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-52 mb-5">
        <FaSpinner className="animate-spin text-4xl" />
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  return (
    <div className="flex justify-center flex-col h-52 mb-5">
      <h2 className="m-4 text-2xl font-bold">Recommendations</h2>
      <ul className="overflow-x-auto flex flex-row gap-1">
        {recommendations.map((recommendation) => (
          <li key={recommendation.product_id} className="w-1/5 flex-none">
            <Link to={`/title/${recommendation.product_slug}`}>
              <img
                src={`http://localhost:8000/api/${recommendation.product_thumbnail}`}
                alt={recommendation.product_name}
                className="object-cover w-full h-full bg-slate-400"
              />
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendations;
