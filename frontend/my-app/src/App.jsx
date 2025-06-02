import { useState, useEffect } from "react";
import "./App.css";
import SkillsSelect from "./components/SkillsSelect";
import MatchResults from "./components/MatchResults";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

function App() {
  const [feedbackPopupOpen, setFeedbackPopupOpen] = useState(false);

  const [userSkills, setUserSkills] = useState();

  const [skillsOptions, setSkillOptions] = useState();

  const [recommendations, setRecommendations] = useState();

  const onSkillsChange = (selectedSkills) => {
    setUserSkills(selectedSkills);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ skills: selectedSkills }),
    };
    
    fetch("http://127.0.0.1:8000/recommend", requestOptions)
      .then((response) => response.json())
      .then((json) => setRecommendations(json.recommendations))
      .catch((error) => console.error(error));
  };


  const onRoleRecommentationLiked = () => {
    setFeedbackPopupOpen(true);
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/available_skills")
      .then((response) => response.json())
      .then((json) => setSkillOptions(json.skills))
      .catch((error) => console.error(error));
  }, []);

  return (
    <>
      <div className="logo-container">
        <img src="logo.svg" alt="Logo" className="logo" />
      </div>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        open={feedbackPopupOpen}
        autoHideDuration={5000}
        onClose={() => setFeedbackPopupOpen(false)}
      >
        <Alert severity="success" variant="filled" sx={{ width: "100%" }}>
          Thank you for your feedback!
        </Alert>
      </Snackbar>
      {skillsOptions && !userSkills && (
        <div>
          <SkillsSelect
            skillsOptions={skillsOptions}
            onSkillsChange={onSkillsChange}
          ></SkillsSelect>
        </div>
      )}


      {recommendations && (
        <div>
          <MatchResults
            roleRecommendations={recommendations}
            onRoleRecommentationLiked={onRoleRecommentationLiked}
          ></MatchResults>
        </div>
      )}
    </>
  );
}

export default App;
