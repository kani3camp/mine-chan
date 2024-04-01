import Image from 'next/image';
import Link from 'next/link';

export default function Home() {
    return (
        <main className="flex flex-col items-center justify-between p-24">
            <h1>まいんちゃんをさがせ！</h1>

            <div className="my-10">
                <Image
                    src="/mine-chan.png"
                    alt="まいんちゃん"
                    width={200}
                    height={200}
                />
            </div>

            <div className="flex flex-col gap-x-1.5">
                <label className="block text-sm font-medium" htmlFor="num_bomb">
                    爆弾数：
                </label>
                <input
                    type="number"
                    id="num_bomb"
                    className="w-full block border border-gray-200 leading-tight focus:outline-none"
                />
                <button className="my-2 p-2.5 bg-transparent hover:bg-pink-500 text-pink-700 font-semibold hover:text-white py-2 px-4 border border-pink-500 hover:border-transparent rounded">
                    ひとりプレイ
                </button>
            </div>

            <Link
                href={'/game'}
                className="bg-pink-500 hover:bg-pink-700 text-white font-bold py-2 px-4 rounded-full"
            >
                ゲーム画面へ
            </Link>
        </main>
    );
}
