import Image from "next/image";

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

      <div className="flex flex-col">
        <label htmlFor="num_bomb">爆弾数</label>
        <input type="number" id="num_bomb" />
        <button>ひとりプレイ</button>
      </div>
    </main>
  );
}
