import GameItem from "./GameItem";

interface GameListProps {
  games: Array<{
    title: string;
    thumbnail_url: string;
    description: string;
    slug: string;
  }>;
}

const GameList = ({ games }: GameListProps) => {
  console.log("Dane w komponencie gamelist:", games);
  return (
    <div className="border h-full border-gray-300 rounded-md p-2 overflow-y-auto">
      {games.map((game, index) => (
        <div key={index} className="p-2">
          <GameItem {...game} />
        </div>
      ))}
    </div>
  );
};

export default GameList;
