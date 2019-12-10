export function modBase1(dividend, divisor) {
    const ret = dividend % divisor;
    if (ret == 0) return divisor;
    else return ret;
}

function createStage(stage, zone) {
    return {
        stage: stage,
        zones: [String(zone)]
    };
}

export function createMatrix() {
    const days = [];
    for (let i = 1; i <= 31; i++) {
        let day = i;
        if (day >= 17) day = i - 16;
        const data = {};
        data["day"] = i;

        const offset = Math.ceil(day / 4);
        let stageBase = modBase1(offset + 12 * (day - 1), 16);
        const blocks = [];
        for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
            const stages = [
                createStage(1, modBase1(stageBase + blockIndex     , 16)),
                createStage(2, modBase1(stageBase + blockIndex + 8 , 16)),
                createStage(3, modBase1(stageBase + blockIndex + 12, 16)),
                createStage(4, modBase1(stageBase + blockIndex + 4 , 16)),
                createStage(5, modBase1(stageBase + blockIndex + 1     , 16)),
                createStage(6, modBase1(stageBase + blockIndex + 8  + 1, 16)),
                createStage(7, modBase1(stageBase + blockIndex + 12 + 1, 16)),
                createStage(8, modBase1(stageBase + blockIndex + 4  + 1, 16))
            ];

            const block = {
                block: blockIndex,
                start: `${String(blockIndex * 2).padStart(2, '0')}:00`,
                end: `${String(blockIndex * 2 + 2).padStart(2, '0')}:30`,
                stages: stages
            };

            blocks.push(block);
        }

        data["blocks"] = blocks;
        days.push(data);
    }

    return {
        "zones": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"],
        matrix: days
    };
}