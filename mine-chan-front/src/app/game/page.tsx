'use client';

import { on } from 'events';

export default function Home() {
    const squares = [
        ['💣', '3', '1', '2', '', '💣', '', '', '3'],
        ['💣', '', '1', '2', '', '💣', '', '', '3'],
        ['💣', '', '1', '2', '', '💣', '💣', '💣', '3'],
        ['💣', '3', '1', '2', '', '💣', '', '', '3'],
        ['💣', '', '1', '2', '', '💣', '', '', '3'],
        ['💣', '', '1', '2', '', '💣', '💣', '💣', '3'],
        ['💣', '3', '1', '2', '', '💣', '', '', '3'],
        ['💣', '', '1', '2', '', '💣', '', '', '3'],
        ['💣', '', '1', '2', '', '💣', '💣', '💣', '3'],
    ];

    const handleClick = (x: number, y: number) => {
        console.log(x, y);
    };

    return (
        <main className=" p-24">
            <h1>ゲーム</h1>

            <div
                id="field"
                className="aspect-square my-10 grid grid-cols-9 gap-1 w-96 h-96 select-none"
            >
                {squares.flat().map((square, i) => {
                    let color;
                    let onClick = () => {};
                    let hover = '';
                    switch (square) {
                        case '💣':
                            color = 'bg-red-600';
                            break;
                        case '':
                            color = 'bg-gray-300';
                            onClick = () =>
                                handleClick(i % 9, Math.floor(i / 9));
                            hover = 'hover:bg-gray-400';
                            break;
                        default:
                            color = 'bg-white text-green-700';
                    }
                    return (
                        <div
                            key={i}
                            className={`text-center  ${color} aspect-square flex items-center justify-center font-bold ${hover}`}
                            onClick={onClick}
                        >
                            <p>{square}</p>
                        </div>
                    );
                })}
            </div>
        </main>
    );
}
