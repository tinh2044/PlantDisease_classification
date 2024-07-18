import { Box, FormControl, InputLabel, MenuItem, Select } from '@mui/material'
import React, { useEffect, useState } from 'react'
import axios from "axios";

function SelectBox({ plant, setPlant, classes }) {
    const [plantDiseases, setPlantDiseases] = useState([])

    const getDisease = async () => {
        let res = await axios.get(`https://serverplantdisease.onrender.com/diseases`);
        setPlantDiseases(res.data)

    }

    useEffect(() => {
        getDisease()
    }, [])
    return (
        <Box style={{ minWidth: 120, maxWidth: 250, width: "100%" }} >
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label" className={classes.label}>Cây trồng</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={plant}
                    label={"Cây trồng"}
                    onChange={(e) => setPlant(e.target.value)}

                >
                    {plantDiseases.map(item => (
                        <MenuItem key={item.key} value={item.key}>{item.name}</MenuItem>
                    ))}

                </Select>
            </FormControl>
        </Box>
    )
}

export default SelectBox