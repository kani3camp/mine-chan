'use client';
import { Configuration, GameApi } from '@/types';
import { set } from 'firebase/database';
import { useState } from 'react';

export default function Home() {
    const [squares, setSquares] = useState<string[]>([]);
    const [gameId, setGameId] = useState<string>('');

    const createNewGame = async () => {
        const api = new GameApi(
            new Configuration({
                basePath: 'http://localhost:8080',
            })
        );
        const res = await api.apiGamePost({
            createGame: {
                numPlayer: 1,
                numMines: 10,
                x: 9,
                y: 9,
            },
        });
        console.log(res);
        setGameId(res);
    };

    const getGame = async () => {
        const api = new GameApi(
            new Configuration({
                basePath: 'http://localhost:8080',
            })
        );
        console.log('gameId', gameId);
        const res = await api.apiGameGameIdGet({
            gameId: gameId,
        });
        setSquares(res.squares);
    };

    const onSquareClick = async (x: number, y: number) => {
        console.log(x, y);
        const api = new GameApi(
            new Configuration({
                basePath: 'http://localhost:8080',
            })
        );
        const res = await api.apiGameGameIdDigPost({
            gameId: gameId,
            digSquare: {
                x: x,
                y: y,
            },
        });
        setSquares(res.squares);

        // ゲームオーバーの場合
        if (res.squares.flat().includes('X')) {
            alert('ゲームオーバー');
        }
    };

    const handleRightClick = async (
        e: React.MouseEvent,
        x: number,
        y: number
    ) => {
        e.preventDefault();

        const api = new GameApi(
            new Configuration({
                basePath: 'http://localhost:8080',
            })
        );
        const res = await api.apiGameGameIdFlagPost({
            gameId: gameId,
            flagSquare: {
                x: x,
                y: y,
            },
        });
        setSquares(res.squares);
    };

    return (
        <main className=" p-24">
            <h1 className="text-2xl font-bold">ゲーム {gameId}</h1>

            <button className="btn block my-1" onClick={createNewGame}>
                ゲーム新規作成
            </button>

            <button className="btn block my-1" onClick={getGame}>
                ゲーム取得
            </button>

            <div
                id="field"
                className="p-1 outline bg-gray-100 aspect-square my-10 grid grid-cols-9 gap-1 w-96 h-96 select-none"
            >
                {squares?.flat().map((square, i) => {
                    let color;
                    let onClick = () => {};
                    let hover = '';
                    let text = '';
                    switch (square) {
                        case 'X':
                            text = '💣';
                            color = 'bg-red-600';
                            break;
                        case '':
                            color = 'bg-gray-300';
                            onClick = () =>
                                onSquareClick(i % 9, Math.floor(i / 9));
                            hover = 'hover:bg-gray-400';
                            break;
                        case '0':
                            color = 'bg-white';
                            break;
                        default:
                            if (square[0] === '_') {
                                if (square[1] === 'X') {
                                    text = '💣';
                                } else {
                                    text = square[1];
                                }
                            } else if (square[0] === 'F') {
                                text = '🚩';
                                color = 'bg-white';
                            } else {
                                text = square;
                                if (square === '1')
                                    color = 'bg-white text-blue-700';
                                if (square === '2')
                                    color = 'bg-white text-green-700';
                                if (square === '3')
                                    color = 'bg-white text-red-700';
                                if (square === '4')
                                    color = 'bg-white text-purple-700';
                                if (square === '5')
                                    color = 'bg-white text-yellow-700';
                                if (square === '6')
                                    color = 'bg-white text-blue-700';
                                if (square === '7')
                                    color = 'bg-white text-green-700';
                                if (square === '8')
                                    color = 'bg-white text-red-700';
                            }
                    }
                    return (
                        <div
                            key={i}
                            className={`text-center  ${color} aspect-square flex items-center justify-center font-bold ${hover}`}
                            onClick={onClick}
                            onContextMenu={(e) => {
                                handleRightClick(e, i % 9, Math.floor(i / 9));
                                return false;
                            }}
                        >
                            <p>{text}</p>
                        </div>
                    );
                })}
            </div>
        </main>
    );
}
