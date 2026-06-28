// StockOne logo: rounded terminal mark + S-shaped market path.
//
// 概念:
//   - 外层框:本地量化工作台 / 终端边界
//   - S 形路径:StockOne 的 S,也是价格走势
//   - 右上节点:突破点 / 当前信号
//
// 用 currentColor,继承父级 color 设定,方便切换品牌色。
interface LogoProps {
  className?: string
  size?: number
  style?: React.CSSProperties
}

export function Logo({ className, size = 32, style }: LogoProps) {
  return (
    <svg
      viewBox="0 0 32 32"
      width={size}
      height={size}
      fill="none"
      className={className}
      style={style}
      role="img"
      aria-label="StockOne"
    >
      <path
        d="M7 4.5h18A2.5 2.5 0 0 1 27.5 7v18a2.5 2.5 0 0 1-2.5 2.5H7A2.5 2.5 0 0 1 4.5 25V7A2.5 2.5 0 0 1 7 4.5Z"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinejoin="round"
        strokeOpacity="0.28"
      />
      <path
        d="M9 20.8c2.1 2.3 6.2 2.5 8.6.9 2.8-1.9 1.7-4.9-1.8-5.6l-2.1-.4c-3.8-.8-4.8-4.2-1.8-6.2 2.6-1.8 7.1-1.1 9.1 1.4"
        stroke="currentColor"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M20.4 10.9 23.5 7.8 26.6 10.9"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle
        cx="23.5"
        cy="7.8"
        r="1.6"
        fill="currentColor"
      />
    </svg>
  )
}
