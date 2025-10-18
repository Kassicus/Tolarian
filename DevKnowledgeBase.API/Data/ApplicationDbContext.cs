using Microsoft.EntityFrameworkCore;
using DevKnowledgeBase.API.Models;

namespace DevKnowledgeBase.API.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Article> Articles { get; set; }
    public DbSet<Category> Categories { get; set; }
    public DbSet<Tag> Tags { get; set; }
    public DbSet<ArticleTag> ArticleTags { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Article configuration
        modelBuilder.Entity<Article>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Title).HasMaxLength(500).IsRequired();
            entity.Property(e => e.Slug).HasMaxLength(500).IsRequired();
            entity.HasIndex(e => e.Slug).IsUnique();
            entity.Property(e => e.Content).IsRequired();
            entity.Property(e => e.CreatedBy).HasMaxLength(100);

            // PostgreSQL Full-Text Search index
            entity.HasIndex(e => e.SearchVector)
                  .HasMethod("GIN");

            // Foreign key to Category
            entity.HasOne(e => e.Category)
                  .WithMany(c => c.Articles)
                  .HasForeignKey(e => e.CategoryId)
                  .OnDelete(DeleteBehavior.SetNull);
        });

        // Category configuration
        modelBuilder.Entity<Category>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).HasMaxLength(200).IsRequired();
            entity.Property(e => e.Slug).HasMaxLength(200).IsRequired();
            entity.HasIndex(e => e.Slug).IsUnique();

            // Self-referencing relationship
            entity.HasOne(e => e.Parent)
                  .WithMany(c => c.Children)
                  .HasForeignKey(e => e.ParentId)
                  .OnDelete(DeleteBehavior.Restrict);
        });

        // Tag configuration
        modelBuilder.Entity<Tag>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).HasMaxLength(100).IsRequired();
            entity.Property(e => e.Slug).HasMaxLength(100).IsRequired();
            entity.HasIndex(e => e.Slug).IsUnique();
        });

        // ArticleTag (many-to-many) configuration
        modelBuilder.Entity<ArticleTag>(entity =>
        {
            entity.HasKey(at => new { at.ArticleId, at.TagId });

            entity.HasOne(at => at.Article)
                  .WithMany(a => a.ArticleTags)
                  .HasForeignKey(at => at.ArticleId)
                  .OnDelete(DeleteBehavior.Cascade);

            entity.HasOne(at => at.Tag)
                  .WithMany(t => t.ArticleTags)
                  .HasForeignKey(at => at.TagId)
                  .OnDelete(DeleteBehavior.Cascade);
        });
    }
}
