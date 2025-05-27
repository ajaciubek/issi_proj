import React, { useState } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

const dummyValues = [
    {
        Role : "Machine Learning Engineer",
        MatchPercent: 98,
        Skills: [
            {Skill: "Python", Status: true},
            {Skill: "Pandas", Status: true},
            {Skill: "pyTorch", Status: true},
            {Skill: "TensorFlow", Status: true},
            {Skill: "Polars", Status: false, SkillGapPercent: 40,}
        ]
    },
    {
        Role : "Python Developer",
        MatchPercent: 69,
        Skills: [
            {Skill: "Python", Status: true},
            {Skill: "Pandas", Status: true},
            {Skill: "Flask", Status: true},
            {Skill: "FastAPI", Status: false, SkillGapPercent: 90},
            {Skill: "SQL Alchemy", Status: false, SkillGapPercent: 11,}
        ]
    }
]

const createRolePanel = (role) => {
    return (
        <Accordion>
        <AccordionSummary
          expandIcon={<ArrowDownwardIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          <Typography component="span">{role.Role}</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget.
          </Typography>
        </AccordionDetails>
      </Accordion>
    )
}


export default function MatchResults({skillsOptions, onSkillsChange}) {

    const roleRecommendations = dummyValues;
    const roleRecommedationsPanels=roleRecommendations.map(createRolePanel
    );

    return (
        <>
        {roleRecommedationsPanels}
        </>
    )
}