type VideoPreviewProps = {
  src: string;
};

export function VideoPreview({ src }: VideoPreviewProps) {
  return (
    <video
      src={src}
      controls
      className="h-36 w-full rounded-2xl bg-black object-cover"
    />
  );
}
