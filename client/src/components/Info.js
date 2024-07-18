import { Accordion, AccordionDetails, AccordionSummary } from '@mui/material'
import React from 'react'

function Info({ data }) {
    console.log(data)
    const { description, agent, symptom } = data.info
    return (
        <div style={{ flexFlow: 1, margin: "2em" }}>
            <Accordion expanded={true} style={{ fontSize: "16px" }}>
                <AccordionSummary aria-controls="panel1-content"
                    id="panel1-header" style={{ fontWeight: "bold", fontSize: "24px" }}>Mô Tả</AccordionSummary>
                <AccordionDetails>{description}</AccordionDetails>
            </Accordion>
            {agent && <Accordion expanded={true}>
                <AccordionSummary
                    aria-controls="panel1-content"
                    id="panel1-header"
                    style={{ fontWeight: "bold", fontSize: "24px" }}
                >Tác nhân</AccordionSummary>
                <AccordionDetails>{agent}</AccordionDetails>
            </Accordion>}
            {symptom && <Accordion expanded={true}>
                <AccordionSummary
                    aria-controls="panel1-content"
                    id="panel1-header"
                    style={{ fontWeight: "bold", fontSize: "24px" }}
                >Chiệu trứng</AccordionSummary>
                <AccordionDetails>{symptom}</AccordionDetails>
            </Accordion>}

        </div>
    )
}

export default Info