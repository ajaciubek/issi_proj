import React, { useState } from 'react';
import Select from 'react-select';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';


export default function SkillsSelect({skillsOptions, onSkillsChange}) {

    const optionKeyValues = skillsOptions.map(op => ({value:op, label:op}))

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
            onSkillsChange(selection.map(skill => skill.value))
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
                    options={optionKeyValues}
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
                        })
                    }}
                    theme={(theme) => ({
                        ...theme,
                        borderRadius: 8,
                        colors: {
                          ...theme.colors,
                          primary25: '#E8E3FF',
                          primary: '#552EEE',
                        },
                      })}

                />
                <button  onClick={onSubmit}>Show directions</button>
            </div>
            <div>
            {displayWarning && <p style= {{color: '#CB0000'}}>
                <ChatBubbleOutlineIcon style={{margin: '0px 0.4em -0.3em 0em'}} />
                Hey! Could you tell me a bit more about your skills?
                That way, I can recommend roles that are a better match for what you're great at.
                </p>}
            </div>
        </div>
    );
}
