import React, { useState } from 'react';
import Select from 'react-select';

export default function SkillsSelect({skillsOptions, onSkillsChange}) {

    const [selection, setSelection] = useState([])
    const [displayWarning, setDisplayWarning] = useState(false)
    const onChange = (
        newValue,
        actionMeta
      ) => {
        setSelection(newValue)
      }
    const onSubmit = () => { 
        if (selection.length <= 3) {
            setDisplayWarning (true)
        }
        else {
            setDisplayWarning (false)
            onSkillsChange(selection)
        }
    }

    return (
        <div>
            <h1>Find your path</h1>
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: '10fr 2fr',
                    alignItems: 'center',
                    gap: '10px',
                }}
            >
                <Select
                    isMulti
                    name="skills"
                    options={skillsOptions}
                    className="basic-multi-select"
                    classNamePrefix="select"
                    onChange={onChange}
                    placeholder="Start entering your skills..."
                    styles={{
                        menu: provided => ({
                            ...provided,
                            textAlign: 'left'
                        }),
                        placeholder: (provided) => ({
                            ...provided,
                            textAlign: 'left',
                        }),
                    }}
                />
                <button onClick={onSubmit}>Show directions</button>
            </div>
            <div>
            {displayWarning && <p>
                    Hey! Could you tell me a bit more about your skills?
            That way, I can recommend roles that are a better match for what you're great at.
                </p>}
            </div>
        </div>
    );
}