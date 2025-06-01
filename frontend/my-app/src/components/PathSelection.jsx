import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";

export default function PathSelection({
  userSkills,
  positionCateogries,
  onCategorySelected,
}) {
  const positionCateogryButtons = positionCateogries.map((category) => {
    return (
      <button onClick={() => onCategorySelected(category)} key={category}>
        {category}
      </button>
    );
  });

  return (
    <div>
      <h1>Find your path</h1>
      <p style={{ color: "#CB0000" }}>
        <ChatBubbleOutlineIcon style={{ margin: "0px 0.4em -0.3em 0em" }} />
        It looks like your skills ({userSkills.join(", ")}) could fit into a few
        different areas. Which one do you think you'd feel most comfortable in?
      </p>
      <div>{positionCateogryButtons}</div>
    </div>
  );
}
