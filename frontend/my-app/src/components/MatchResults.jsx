import React, { useState } from "react";
import Accordion from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import Typography from "@mui/material/Typography";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import ThumbUpOffAltIcon from "@mui/icons-material/ThumbUpOffAlt";
import ThumbUpAltIcon from "@mui/icons-material/ThumbUpAlt";

const createRolePanel = (role, onRoleRecommentationLiked) => {
  const [liked, setLiked] = useState(false);

  return (
    <div class="match_results" key={role.role}>
      <Accordion style={{ borderRadius: 8, color: "#474747" }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
          style={{
            backgroundColor: calculateColor(role.matchPercent),
            borderRadius: 8,
            border: `1px solid ${calculateBorderColor(role.matchPercent)}`,
            outline: "none",
          }}
        >
          <Typography component="span" style={{ fontWeight: "bold" }}>
            {role.role}
          </Typography>
          <Typography
            component="span"
            style={{ margin: "0 0.5em", color: "gray", flex: 1 }}
          >
            ({role.matchPercent}% match)
          </Typography>

          {liked ? (
            <ThumbUpAltIcon
              onClick={(e) => {
                e.stopPropagation();
              }}
            />
          ) : (
            <ThumbUpOffAltIcon
              onClick={(e) => {
                onRoleRecommentationLiked(role);
                setLiked(true);
                e.stopPropagation();
              }}
            />
          )}
        </AccordionSummary>

        <AccordionDetails>
          <ul>{createRoleSkills(role.skills)}</ul>
        </AccordionDetails>
      </Accordion>
    </div>
  );
};
const createRoleSkills = (skills) => {
  return skills.map((skill) => (
    <li key={skill.skill}>
      {skill.status ? (
        <CheckIcon style={{ color: "limegreen" }}></CheckIcon>
      ) : (
        <CloseIcon style={{ color: "red" }}></CloseIcon>
      )}

      <span className="name">{skill.skill}</span>
      {skill.skillGapPercent && (
        <span class="gap" style={{ margin: "0 0.5em", color: "gray" }}>
          {skill.skillGapPercent}% chance this skill is required for this role.
        </span>
      )}
    </li>
  ));
};

const calculateColor = (matchPercent) => {
  if (matchPercent >= 91) return "#BBFFCF";
  if (matchPercent >= 76) return "#DCFFBB";
  if (matchPercent >= 66) return "#FFF1AA";
  if (matchPercent >= 51) return "#FFD39A";
  return "#FFBBBB";
};

const calculateBorderColor = (matchPercent) => {
  if (matchPercent >= 91) return "#13D671";
  if (matchPercent >= 76) return "#59C307";
  if (matchPercent >= 66) return "#FFBF00";
  if (matchPercent >= 51) return "#EE8E11";
  return "#E30000";
};

export default function MatchResults({
  roleRecommendations,
  onRoleRecommentationLiked,
}) {
  const roleRecommedationsPanels = roleRecommendations.map((role) =>
    createRolePanel(role, onRoleRecommentationLiked)
  );

  return (
    <>
      <h1>Pefect match!</h1>
      <p style={{ color: "#00A14E" }}>
        <ChatBubbleOutlineIcon style={{ margin: "0px 0.4em -0.3em 0em" }} />
        Here are some roles that match your skills best. Click to see details,
        and give a thumbs up to the ones you like — it helps me learn and
        improve future matches!
      </p>
      {roleRecommedationsPanels}
    </>
  );
}
