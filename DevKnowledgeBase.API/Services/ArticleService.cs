using Microsoft.EntityFrameworkCore;
using DevKnowledgeBase.API.Data;
using DevKnowledgeBase.API.Models;
using DevKnowledgeBase.API.DTOs;

namespace DevKnowledgeBase.API.Services;

public class ArticleService
{
    private readonly ApplicationDbContext _context;

    public ArticleService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<List<ArticleDto>> GetAllArticlesAsync(int page = 1, int pageSize = 20)
    {
        var articles = await _context.Articles
            .Include(a => a.Category)
            .Include(a => a.ArticleTags)
                .ThenInclude(at => at.Tag)
            .OrderByDescending(a => a.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return articles.Select(MapToDto).ToList();
    }

    public async Task<ArticleDto?> GetArticleByIdAsync(Guid id)
    {
        var article = await _context.Articles
            .Include(a => a.Category)
            .Include(a => a.ArticleTags)
                .ThenInclude(at => at.Tag)
            .FirstOrDefaultAsync(a => a.Id == id);

        return article == null ? null : MapToDto(article);
    }

    public async Task<ArticleDto?> GetArticleBySlugAsync(string slug)
    {
        var article = await _context.Articles
            .Include(a => a.Category)
            .Include(a => a.ArticleTags)
                .ThenInclude(at => at.Tag)
            .FirstOrDefaultAsync(a => a.Slug == slug);

        return article == null ? null : MapToDto(article);
    }

    public async Task<ArticleDto> CreateArticleAsync(CreateArticleDto createDto)
    {
        var article = new Article
        {
            Id = Guid.NewGuid(),
            Title = createDto.Title,
            Slug = GenerateSlug(createDto.Title),
            Content = createDto.Content,
            CategoryId = createDto.CategoryId,
            CreatedBy = createDto.CreatedBy,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        _context.Articles.Add(article);

        // Add tags
        foreach (var tagId in createDto.TagIds)
        {
            _context.ArticleTags.Add(new ArticleTag
            {
                ArticleId = article.Id,
                TagId = tagId
            });
        }

        await _context.SaveChangesAsync();

        return (await GetArticleByIdAsync(article.Id))!;
    }

    public async Task<ArticleDto?> UpdateArticleAsync(Guid id, UpdateArticleDto updateDto)
    {
        var article = await _context.Articles
            .Include(a => a.ArticleTags)
            .FirstOrDefaultAsync(a => a.Id == id);

        if (article == null)
            return null;

        article.Title = updateDto.Title;
        article.Slug = GenerateSlug(updateDto.Title);
        article.Content = updateDto.Content;
        article.CategoryId = updateDto.CategoryId;
        article.UpdatedAt = DateTime.UtcNow;

        // Update tags: remove old, add new
        _context.ArticleTags.RemoveRange(article.ArticleTags);
        foreach (var tagId in updateDto.TagIds)
        {
            _context.ArticleTags.Add(new ArticleTag
            {
                ArticleId = article.Id,
                TagId = tagId
            });
        }

        await _context.SaveChangesAsync();

        return await GetArticleByIdAsync(id);
    }

    public async Task<bool> DeleteArticleAsync(Guid id)
    {
        var article = await _context.Articles.FindAsync(id);
        if (article == null)
            return false;

        _context.Articles.Remove(article);
        await _context.SaveChangesAsync();
        return true;
    }

    private ArticleDto MapToDto(Article article)
    {
        return new ArticleDto
        {
            Id = article.Id,
            Title = article.Title,
            Slug = article.Slug,
            Content = article.Content,
            CategoryId = article.CategoryId,
            CategoryName = article.Category?.Name,
            CreatedAt = article.CreatedAt,
            UpdatedAt = article.UpdatedAt,
            CreatedBy = article.CreatedBy,
            Tags = article.ArticleTags.Select(at => new TagDto
            {
                Id = at.Tag.Id,
                Name = at.Tag.Name,
                Slug = at.Tag.Slug
            }).ToList()
        };
    }

    private string GenerateSlug(string title)
    {
        var slug = title.ToLowerInvariant()
            .Replace(" ", "-")
            .Replace("'", "")
            .Replace("\"", "");

        // Remove non-alphanumeric characters except hyphens
        slug = new string(slug.Where(c => char.IsLetterOrDigit(c) || c == '-').ToArray());

        // Add timestamp to ensure uniqueness
        return $"{slug}-{DateTime.UtcNow.Ticks}";
    }
}
