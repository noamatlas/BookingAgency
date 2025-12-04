import React, { useState, useEffect } from 'react';
import { sendHttpPost } from './sendHttpReq.js';

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Input from '@mui/material/Input';

export const AskAiComp = () => {
    const [loading, setLoading] = useState(false);
    const [optionGroupValue, setOptionGroupValue] = useState('countries');
    const [aiAnswer, setAiAnswer] = useState("");
    const [dest, setDest] = useState("");
    const [free, setFree] = useState("");

    const handleChange = (event) => {
        setAiAnswer("");
        setOptionGroupValue(event.target.value);
    }
    const changeDest = (event) => {
        setDest(event.target.value);
    }
    const changeFree = (event) => {
        setFree(event.target.value);
    }

    const doYourJob = async () => {
        try {
            setAiAnswer("");
            if (optionGroupValue == '') return alert('You have to choose one of the options.');
            if (optionGroupValue == 'vacations' && dest == '') return alert('You have to write the desired destination.');
            if (optionGroupValue == 'free' && free == '') return alert('You have to write a prompt to the AI.');

            setLoading(true);
            let promptText = "";
            let pathSuffix = '';

            switch (optionGroupValue) {
                case 'countries':
                    setDest("");
                    setFree("");
                    promptText = 'What are the valid countries in the database?';
                    pathSuffix = 'ai_travel';
                    break;
                case 'vacations':
                    setFree("");
                    promptText = `Get vacations for a given country name: ${dest}.`;
                    pathSuffix = 'ai_travel';
                    break;
                default:
                    setDest("");
                    promptText = free;
                    pathSuffix = 'ai_general';
                    break;
            }
            const response = await sendHttpPost(promptText, pathSuffix);
            setAiAnswer(response);
            setLoading(false);
        } catch (error) {
            setAiAnswer(error.message);
        }
    }

    return (
        <>
            <FormControl style={{ textAlign: 'left', marginTop: '6vh', marginLeft: '4vw' }}>
                <Typography variant="h6" style={{ color: 'black', width: '80%' }}>
                    OUR VACATIONS AND SERVICES
                </Typography>
                <FormLabel id="demo-controlled-radio-buttons-group" style={{ color: 'black' }}>Ask the AI Agent</FormLabel>
                <RadioGroup
                    name="controlled-radio-buttons-group" value={optionGroupValue} onChange={handleChange}
                >
                    <FormControlLabel value="countries" control={<Radio />} label="Show available countries for vacations" />
                    <FormControlLabel value="vacations" control={<Radio />} label="Find vacations for a destination:" />
                    <Input value={dest} style={{ marginTop: 0, paddingTop: 0 }} onChange={changeDest} />
                    <FormControlLabel value="free" control={<Radio />} label="Ask a free question on any subject:" />
                    <Input value={free} style={{ marginTop: 0, paddingTop: 0 }} onChange={changeFree} />
                </RadioGroup>
                <Box sx={{ width: '100%', maxWidth: 500 }}>
                    <Button onClick={doYourJob} sx={{ mt: 2, mr: 1, mb: 1 }} type="button" variant="contained">
                        See AI Answer
                    </Button>
                    <Typography variant="h6">
                        AI Answer:
                    </Typography>
                    {loading && (
                        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100px' }}>
                            <CircularProgress size={40} thickness={6} style={{ color: 'white' }} />
                        </Box>
                    )}
                    <Typography variant="subtitle1" style={{ color: 'white', width: '80%', maxHeight: '32vh', overflowY: 'auto' }}>
                        {aiAnswer}
                    </Typography>
                </Box>
            </FormControl>
        </>
    );
}