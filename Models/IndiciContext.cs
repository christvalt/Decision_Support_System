using Microsoft.EntityFrameworkCore;
namespace SsdWebApi.Models
{
    public class IndiceContext : DbContext
    {
        public IndiceContext(DbContextOptions<IndiceContext> options)
        : base(options)
        {
        }
        public DbSet<Indici> indici { get; set; }
    }
}
