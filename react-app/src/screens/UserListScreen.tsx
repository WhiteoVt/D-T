import GameList from "../components/ListComponents/GameList";
import { useEffect, useState } from "react";
import { useAuth } from "../AuthContext";

const UserListScreen = () => {
  const { token } = useAuth();
  const [fetchedProducts, setFetchedProducts] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = "http://localhost:8000/api/ownedproduct/";
        const response = await fetch(url, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        if (!response.ok) {
          console.error("Błąd pobierania danych:", response);
          return;
        }

        const data = await response.json();

        if (Array.isArray(data)) {
          setFetchedProducts(data);
          console.log("Dane pobrane z serwera:", data);
        } else {
          console.error("Błąd w strukturze danych:", data);
        }
      } catch (error) {
        console.error("Błąd pobierania danych:", error);
      }
    };

    fetchData();
  }, [token]);

  return (
    <div className="m-4 p-4">
      <h2>My collection</h2>
      {fetchedProducts && fetchedProducts.length > 0 ? (
        <GameList
          games={fetchedProducts.map((product) => ({
            title: product.slug,
            thumbnail_url: product.thumbnail_url,
            description: product.description,
            slug: product.slug,
          }))}
        />
      ) : (
        <p>No games in the collection.</p>
      )}
    </div>
  );
};

export default UserListScreen;
