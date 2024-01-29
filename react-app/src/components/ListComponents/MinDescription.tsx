
interface Props {
  text: string;
  maxLength: number;
}

const MinDescription = ({ text, maxLength }: Props) => {
  const shortenedText = text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;

  return (
    <p className="description-text">
      {shortenedText}
    </p>
  );
};

export default MinDescription;