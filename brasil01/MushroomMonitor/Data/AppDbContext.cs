using Microsoft.EntityFrameworkCore;
using MushroomMonitor.Models;

namespace MushroomMonitor.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<EnvironmentLog> EnvironmentLogs { get; set; }
    }
}
