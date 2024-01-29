import GameList from "../components/ListComponents/GameList";
import { useEffect, useState } from "react";

const GameListScreen = () => {
  const [fetchedProducts, setFetchedProducts] = useState<any[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [searchText, setSearchText] = useState<string>("");
  const [notFoundMessage, setNotFoundMessage] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const url = `http://localhost:8000/api/products/?page=${currentPage}&page_size=10&name=${searchText}`;
      const response = await fetch(url);
      const data = await response.json();

      const products = data.results || [];
      setFetchedProducts((prevProducts) => [...prevProducts, ...products]);

      if (products.length === 0 && currentPage === 1) {
        setNotFoundMessage("Game not found. Try again");
      } else {
        setNotFoundMessage(null);
      }
    } catch (error) {
      console.error("Błąd pobierania danych:", error);
    }
  };

  const loadMore = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };

  const handleSearch = () => {
    setCurrentPage(1);
    setFetchedProducts([]);
    setNotFoundMessage(null);
    fetchData();
  };

  const resetList = () => {
    setSearchText("");
    setCurrentPage(1);
    setFetchedProducts([]);
    setNotFoundMessage(null);
    fetchData();
  };

  useEffect(() => {
    fetchData();
  }, [currentPage, searchText]);

  return (
    <div className="m-4 p-4">
      <h2 className="m-10 text-xl">Game list</h2>
      <input
        className="m-4 mb-10 p-2 border border-gray-300 rounded-md"
        type="text"
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        placeholder="Enter the game"
      />
      <button
        className="m-4 bg-blue-500 text-white p-2 rounded-md"
        onClick={handleSearch}
      >
        Search
      </button>
      <button
        className="m-4 bg-blue-500 text-white p-2 rounded-md"
        onClick={resetList}
      >
        Restore main list
      </button>

      {notFoundMessage ? (
        <p className="mt-10 text-red-500">{notFoundMessage}</p>
      ) : (
        <GameList
          games={fetchedProducts.map((product) => ({
            title: product.name,
            thumbnail_url: product.thumbnail,
            description: product.description,
            slug: product.slug,
          }))}
        />
      )}

      {fetchedProducts.length > 0 && (
        <button onClick={loadMore}>Load More</button>
      )}
    </div>
  );
};

export default GameListScreen;
