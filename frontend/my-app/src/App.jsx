import { useState } from 'react'
import './App.css'
import PathSelection from './components/pathselection'
import SkillsSelect from './components/SkillsSelect'
import MatchResults from './components/MatchResults'


function App() {
  const [userSkills, setUserSkills] = useState()
  const [positionCateogries, setPositionCategories] = useState(["Backend", "Data Science", "Databases"])
  const defaultSkillOptions = [
    {value: "1", label: "python"},
    {value: "2", label: "api"},
    {value: "3", label: "pandas"},
    {value: "4", label: "pyTorch"}
  ]
  const [skillsOptions, setSkills] = useState(defaultSkillOptions)
  const defaultRecommendations = [
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
  const [recommendations, setRecommendations] = useState()
  
  
  const onSkillsChange = (selectedSkills) => setUserSkills(selectedSkills)
  const onCategorySelected = (selectedCategpory) => setRecommendations(defaultRecommendations)

  
  return (
    <>
      
      { !userSkills && <div>
        <SkillsSelect skillsOptions={skillsOptions} onSkillsChange={onSkillsChange}></SkillsSelect>
      </div> }

      { userSkills && !recommendations && <div>
        <PathSelection userSkills={userSkills} positionCateogries={positionCateogries} onCategorySelected={onCategorySelected}></PathSelection>
      </div> }
      {recommendations && <div>
        <MatchResults roleRecommendations={recommendations}></MatchResults>
      </div> }
    </>
  )
}

export default App
