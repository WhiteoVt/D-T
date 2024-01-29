import GameList from "../components/ListComponents/GameList";

import { useEffect, useState } from "react";

const MainScreen = () => {
  const [fetchedProductsNew, setFetchedProductsNew] = useState<any[]>([]);
  const [fetchedProductsHot, setFetchedProductsHot] = useState<any[]>([]);
  const [currentPageNew, setCurrentPageNew] = useState<number>(1);
  const [currentPageHot, setCurrentPageHot] = useState<number>(1);

  useEffect(() => {
    const fetchDataNew = async () => {
      try {
        const url = `http://localhost:8000/api/products/?page=${currentPageNew}&page_size=5&sort_by=id_desc`;
        const response = await fetch(url);
        const data = await response.json();

        const products = data.results || [];
        setFetchedProductsNew((prevProducts) => [...prevProducts, ...products]);
      } catch (error) {
        console.error("Błąd pobierania danych:", error);
      }
    };

    fetchDataNew();
  }, [currentPageNew]);

  useEffect(() => {
    const fetchDataHot = async () => {
      try {
        const url = `http://localhost:8000/api/products/?page=${currentPageHot}&page_size=5&sort_by=upvotes`;
        const response = await fetch(url);
        const data = await response.json();

        const products = data.results || [];
        setFetchedProductsHot((prevProducts) => [...prevProducts, ...products]);
      } catch (error) {
        console.error("Błąd pobierania danych:", error);
      }
    };

    fetchDataHot();
  }, [currentPageHot]);

  const loadMoreNew = () => {
    // Increment the current page
    setCurrentPageNew((prevPage) => prevPage + 1);
  };

  const loadMoreHot = () => {
    // Increment the current page
    setCurrentPageHot((prevPage) => prevPage + 1);
  };

  return (
    <div className="flex h-screen">
      <div className="w-1/2 h-4/6 m-2">
        <h2 className="text-2xl font-bold">What's new?</h2>
        <GameList
          games={fetchedProductsNew.map((product) => ({
            title: product.name,
            thumbnail_url: product.thumbnail,
            description: product.description,
            slug: product.slug,
          }))}
        />
        <button
          className="bg-[#0a192f] text-gray-300 p-2 rounded-md"
          onClick={loadMoreNew}
        >
          Load More
        </button>
      </div>
      <div className="w-1/2 h-4/6 m-2">
        <h2 className="text-2xl font-bold">Top for this week</h2>
        <GameList
          games={fetchedProductsHot.map((product) => ({
            title: product.name,
            thumbnail_url: product.thumbnail,
            description: product.description,
            slug: product.slug,
          }))}
        />
        <button
          className="bg-[#0a192f] text-gray-300 p-2 rounded-md"
          onClick={loadMoreHot}
        >
          Load More
        </button>
      </div>
    </div>
  );
};

export default MainScreen;
