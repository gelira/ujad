export function formatDate(dateString: string) {
  const dt = new Date(dateString)

  const date = dt.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })

  const time = dt.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit'
  })

  return `${date} às ${time}`
}