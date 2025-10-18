using NpgsqlTypes;

namespace DevKnowledgeBase.API.Models;

public class Article
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public Guid? CategoryId { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public string? CreatedBy { get; set; }

    // Full-text search vector (PostgreSQL specific)
    public NpgsqlTsVector? SearchVector { get; set; }

    // Navigation properties
    public Category? Category { get; set; }
    public ICollection<ArticleTag> ArticleTags { get; set; } = new List<ArticleTag>();
}
