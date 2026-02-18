import { FunctionTool, LlmAgent } from '@google/adk';
import { z } from 'zod';

const getCurrentTime = new FunctionTool({
    name: 'get_current_time',
    description: 'Returns the current time in a specified city.',
    parameters: z.object({
        city: z.string().describe("The name of the city for which to retrieve the current time."),
    }),
    execute: ({ city }: { city: string }) => {
        return { status: 'success', report: `The current time in ${city} is 10:30 AM` };
    },
});

export const dashboardAgent = new LlmAgent({
    name: 'dashboard_agent',
    model: 'gemini-2.5-flash',
    instruction: `
        You are a UI Architect. Your job is to generate JSX react code for dashboard widgets.
        When a user asks for a component, return ONLY the raw TSX code for a functional component.
        Do not use external libraries other than ReCharts'.
        The component should be self-contained based on the input data.
    `,
});

export const rootAgent = new LlmAgent({
    name: 'orchestrator_agent',
    model: 'gemini-2.5-flash',
    description: 'Tells the current time in a specified city.',
    instruction: `You are a helpful assistant that tells the current time in a city.
                Use the 'getCurrentTime' tool for this purpose.`,
    tools: [getCurrentTime],
});


