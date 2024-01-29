interface Props {
  description: string;
}

const Description = ({ description }: Props) => {
  return (
    <div className="mb-5">
      <h3 className="m-4 text-2xl font-bold">Description</h3>
      <p className="description-text">{description}</p>
    </div>
  );
};

export default Description;
