export function modBase1(dividend, divisor) {
    const ret = dividend % divisor;
    if (ret == 0) return divisor;
    else return ret;
}

function tableData() {
    const rows = [];
    if (this.days.length == 0) return [];

    for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
        const row = {};

        row["block"] = `${blockIndex * 2}:00-${(blockIndex + 1) * 2}:30`;

        let dayStart = this.selectedDate.getDate() - 1;
        for (let day = 0; day < 7; day += 1) {
            const dayData = this.days[dayStart + day];
            if (dayData != null)
                row[`day${day}`] = dayData.blocks[blockIndex];
        }

        rows.push(row);
    }
    return rows;
}

export function createMatrix() {
    console.log("Creating matrix");
    const days = [];
    for (let i = 1; i <= 31; i++) {
        let day = i;
        if (day >= 17) day = i - 16;
        const data = {};
        data["day"] = i;

        data["offset"] = Math.ceil(day / 4);
        let stageBase = modBase1(data["offset"] + 12 * (day - 1), 16);
        const blocks = [];
        for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
            const block = {
                "1": modBase1(stageBase + blockIndex     , 16),
                "2": modBase1(stageBase + blockIndex + 8 , 16),
                "3": modBase1(stageBase + blockIndex + 12, 16),
                "4": modBase1(stageBase + blockIndex + 4 , 16),
                "5": modBase1(stageBase + blockIndex + 1     , 16),
                "6": modBase1(stageBase + blockIndex + 8  + 1, 16),
                "7": modBase1(stageBase + blockIndex + 12 + 1, 16),
                "8": modBase1(stageBase + blockIndex + 4  + 1, 16)
            };

            blocks.push(block);
        }

        data["blocks"] = blocks;
        days.push(data);
    }

    return days;
}