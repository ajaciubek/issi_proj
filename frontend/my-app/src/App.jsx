import { useState, useEffect } from 'react'
import './App.css'
import PathSelection from './components/pathselection'
import SkillsSelect from './components/SkillsSelect'
import MatchResults from './components/MatchResults'



function App() {

  const [userSkills, setUserSkills] = useState()
  const [positionCateogries, setPositionCategories] = useState()
  
  const [skillsOptions, setSkillOptions] = useState()
  
  const [recommendations, setRecommendations] = useState()
  
  
  const onSkillsChange = (selectedSkills) => { 
    setUserSkills(selectedSkills)
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skills: selectedSkills })
  };

    fetch('http://127.0.0.1:8000/suggest_category', requestOptions)
    .then(response => response.json())
    .then(json => setPositionCategories(json.categories))
    .catch(error => console.error(error));
  }

  const onCategorySelected = (selectedCategpory) => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skills: userSkills, category: selectedCategpory })
  };

    fetch('http://127.0.0.1:8000/recommend', requestOptions)
    .then(response => response.json())
    .then(json => setRecommendations(json.recommendations))
    .catch(error => console.error(error));
  }


  useEffect(() => {
    fetch('http://127.0.0.1:8000/available_skills')
      .then(response => response.json())
      .then(json => setSkillOptions(json.skills))
      .catch(error => console.error(error));
  }, []);


  return (
    <>    
      { skillsOptions && !userSkills && <div>
        <SkillsSelect skillsOptions={skillsOptions} onSkillsChange={onSkillsChange}></SkillsSelect>
      </div> }

      { positionCateogries && !recommendations && <div>
        <PathSelection userSkills={userSkills} positionCateogries={positionCateogries} onCategorySelected={onCategorySelected}></PathSelection>
      </div> }
      
      {recommendations && <div>
        <MatchResults roleRecommendations={recommendations}></MatchResults>
      </div> }
    </>
  )
}

export default App
