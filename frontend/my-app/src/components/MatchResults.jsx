import React, { useState } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';



const createRolePanel = (role) => {
    return (
        <div class="match_results" key={role.role}>
        <Accordion >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
          style={{ backgroundColor: calculateColor(role.matchPercent) }}
        >
          <Typography component="span" >{role.role}</Typography>
          <Typography component="span" style={{margin: '0 0.5em', color:'gray'}} >({role.matchPercent}% match)</Typography>

        </AccordionSummary>
        <AccordionDetails>
            <ul>
          {createRoleSkills(role.skills)}
          </ul>
        </AccordionDetails>
      </Accordion>
      </div>
    )
}
const createRoleSkills = (skills) => {
    return skills.map(skill => 
        <li key={skill.skill} >
            {skill.status 
                ? <CheckIcon style={{ color: 'limegreen' }} ></CheckIcon> 
                : <CloseIcon style={{ color: 'red' }}></CloseIcon>  }

            <span className="name">{skill.skill}</span>
            { skill.skillGapPercent && <span class="gap" style={{margin: '0 0.5em', color:'gray'}}>{skill.skillGapPercent}% chance this skill is required for this role.</span> }
        </li>) 

}

const calculateColor = (matchPercent) => {
    if (matchPercent >= 91) return "#BBFFCF";
    if (matchPercent >= 76) return "#DCFFBB";
    if (matchPercent >= 66) return "#FFF1AA";
    if (matchPercent >= 51) return "#FFD39A";
    return "#FFBBBB";
}


export default function MatchResults({roleRecommendations}) {
    const roleRecommedationsPanels=roleRecommendations.map(createRolePanel
    );

    return (
        <>
        <h1>Pefect match!</h1>
        <div style= {{color: 'green'}}>
            <ChatBubbleOutlineIcon style={{margin: '0px 0.4em -0.3em -2em'}} />
            Here are some roles that match your skills best. Click to see details, and give a thumbs up 
        to the ones you like — it helps me learn and improve future matches!
        </div>
        {roleRecommedationsPanels}
        </>
    )
}